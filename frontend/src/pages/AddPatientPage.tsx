import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import Header from '@components/Layout/Header';
import Footer from '@components/Layout/Footer';
import AddPatientForm from '@components/Forms/AddPatientForm';
import { apiClient } from '@services/api';
import type { CreatePatientRequest } from '../types/patient';

export const AddPatientPage = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const handleAddPatient = async (data: CreatePatientRequest) => {
    setIsLoading(true);
    try {
      await apiClient.createPatient(data);
      navigate('/');
    } catch (err) {
      console.error('Failed to add patient:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-slate-50">
      <Header />

      <main className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-2xl">
          <AddPatientForm
            onSubmit={handleAddPatient}
            onClose={() => navigate('/')}
            isLoading={isLoading}
          />
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default AddPatientPage;
