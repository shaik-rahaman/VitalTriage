"""
MongoDB connection and database utilities.
"""
import asyncio
import logging
import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError

logger = logging.getLogger(__name__)

# Global database and client connection
db: AsyncIOMotorDatabase = None
client: AsyncIOMotorClient = None
demo_mode: bool = False  # Flag to indicate if running in demo mode

# In-memory demo data storage
demo_patients = {}


async def connect_to_mongo() -> AsyncIOMotorDatabase:
    """
    Connect to MongoDB with multiple fallback options.
    
    Returns:
        AsyncIOMotorDatabase instance
    """
    global db, client, demo_mode
    
    # Support both old and new environment variable names
    mongo_uri = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME") or os.getenv("MONGO_DB_NAME", "vitaltriage_db")
    
    # Connection attempt list
    connection_attempts = []
    
    # Add the primary connection if provided
    if mongo_uri:
        # Use MongoDB URI as-is (don't append parameters if already present)
        connection_attempts.append(("MongoDB Atlas (SRV)", mongo_uri))
    
    # Add fallback attempt for local MongoDB
    connection_attempts.append(("Local MongoDB", "mongodb://localhost:27017"))
    
    last_error = None
    
    for label, uri in connection_attempts:
        try:
            logger.info(f"[{label}] Attempting connection...")
            
            # Use shorter timeouts for cloud connection, longer for local
            if "mongodb+srv" in uri:
                client = AsyncIOMotorClient(
                    uri,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000,
                    retryWrites=False
                )
            else:
                client = AsyncIOMotorClient(
                    uri,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=10000
                )
            
            # Verify connection with timeout
            try:
                await asyncio.wait_for(client.admin.command('ping'), timeout=10)
                db = client[db_name]
                demo_mode = False
                logger.info(f"✓ [{label}] Connected to MongoDB: {db_name}")
                
                # Create indexes
                try:
                    await create_indexes()
                except Exception as idx_err:
                    logger.warning(f"Index creation warning: {idx_err}")
                
                return db
                
            except (asyncio.TimeoutError, Exception) as conn_err:
                last_error = conn_err
                logger.warning(f"✗ [{label}] Connection failed: {str(conn_err)[:100]}...")
                if client:
                    try:
                        client.close()
                    except:
                        pass
                continue
                
        except Exception as e:
            last_error = e
            logger.warning(f"✗ [{label}] Error: {str(e)[:100]}...")
            if client:
                try:
                    client.close()
                except:
                    pass
            continue
    
    # If all connections fail, log warning but continue in demo mode
    logger.warning("=" * 60)
    logger.warning("⚠️  MongoDB connection failed on all attempts")
    logger.warning("Last error: " + str(last_error)[:100])
    logger.warning("=" * 60)
    logger.warning("SOLUTIONS:")
    logger.warning("1. Check network: DNS and firewall settings")
    logger.warning("2. Start local MongoDB: brew services start mongodb-community")
    logger.warning("3. Or use Docker: docker run -d -p 27017:27017 mongo:latest")
    logger.warning("=" * 60)
    logger.warning("Starting in DEMO MODE - data will be stored in memory only")
    logger.warning("=" * 60)
    
    demo_mode = True
    return None  # Return None to indicate demo mode



async def close_mongo_connection():
    """Close MongoDB connection."""
    global client
    if client is not None:
        client.close()
        logger.info("MongoDB connection closed")


async def create_indexes():
    """Create necessary indexes in MongoDB."""
    try:
        collection = db["patients"]
        
        # Create indexes with timeout
        try:
            await asyncio.wait_for(collection.create_index([("patient_id", ASCENDING)], unique=True), timeout=5)
            await asyncio.wait_for(collection.create_index([("severity", ASCENDING)]), timeout=5)
            await asyncio.wait_for(collection.create_index([("timestamp", DESCENDING)]), timeout=5)
            await asyncio.wait_for(collection.create_index([("score", DESCENDING)]), timeout=5)
            logger.info("Indexes created successfully")
        except asyncio.TimeoutError:
            logger.warning("Index creation timeout - indexes may not have been created")
    except Exception as e:
        logger.warning(f"Failed to create indexes: {str(e)} - proceeding anyway")


async def get_patient_collection():
    """Get the patients collection."""
    if db is None:
        raise RuntimeError("MongoDB not connected")
    return db["patients"]


async def insert_patient(patient_doc: dict):
    """
    Insert a patient document.
    
    Args:
        patient_doc: Patient document
        
    Returns:
        Inserted document ID
    """
    collection = await get_patient_collection()
    try:
        result = await collection.insert_one(patient_doc)
        logger.info(f"Patient inserted: {result.inserted_id}")
        return result.inserted_id
    except DuplicateKeyError:
        logger.error(f"Patient {patient_doc.get('patient_id')} already exists")
        raise


async def update_patient(patient_id: str, update_doc: dict):
    """
    Update a patient document.
    
    Args:
        patient_id: Patient ID
        update_doc: Update document
        
    Returns:
        UpdateResult
    """
    collection = await get_patient_collection()
    logger.debug(f"📝 Updating patient {patient_id} with: {list(update_doc.keys())}")
    result = await collection.update_one(
        {"patient_id": patient_id},
        {"$set": update_doc}
    )
    logger.info(f"✓ Patient {patient_id} update: matched={result.matched_count}, modified={result.modified_count}")
    return result


async def get_patient_by_id(patient_id: str):
    """
    Get a patient by ID.
    
    Args:
        patient_id: Patient ID
        
    Returns:
        Patient document or None
    """
    collection = await get_patient_collection()
    logger.debug(f"🔍 Searching for patient: {patient_id}")
    patient = await collection.find_one({"patient_id": patient_id})
    if patient:
        logger.debug(f"✓ Found patient: {patient_id}")
    else:
        logger.warning(f"⚠️ Patient not found: {patient_id}")
    return patient


async def get_all_patients():
    """
    Get all patients.
    
    Returns:
        List of patient documents
    """
    collection = await get_patient_collection()
    patients = await collection.find().to_list(None)
    return patients


async def get_patients_by_severity(severity: str):
    """
    Get patients by severity.
    
    Args:
        severity: Severity level
        
    Returns:
        List of patient documents
    """
    collection = await get_patient_collection()
    patients = await collection.find({"severity": severity}).to_list(None)
    return patients


async def get_patients_sorted_by_timestamp(limit: int = None):
    """
    Get patients sorted by timestamp (newest first).
    
    Args:
        limit: Maximum number of patients to return
        
    Returns:
        List of patient documents
    """
    collection = await get_patient_collection()
    query = collection.find().sort("timestamp", DESCENDING)
    if limit:
        query = query.limit(limit)
    patients = await query.to_list(None)
    return patients


async def delete_patient(patient_id: str):
    """
    Delete a patient.
    
    Args:
        patient_id: Patient ID
        
    Returns:
        DeleteResult
    """
    collection = await get_patient_collection()
    result = await collection.delete_one({"patient_id": patient_id})
    logger.info(f"Patient {patient_id} deleted: deleted_count={result.deleted_count}")
    return result


async def clear_all_patients():
    """
    Clear all patients (use with caution).
    
    Returns:
        DeleteResult
    """
    collection = await get_patient_collection()
    result = await collection.delete_many({})
    logger.warning(f"All patients cleared: deleted_count={result.deleted_count}")
    return result
