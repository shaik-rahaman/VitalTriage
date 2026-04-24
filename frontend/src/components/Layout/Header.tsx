import { Activity } from 'lucide-react';

export const Header = () => {
  return (
    <header className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Activity className="w-8 h-8 text-red-600" />
          <h1 className="text-2xl font-bold text-slate-900">VitalTriage</h1>
          <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded-full ml-2 font-semibold">
            Hospital Dashboard
          </span>
        </div>
        <div className="text-sm text-slate-500">
          Real-time Patient Monitoring System
        </div>
      </div>
    </header>
  );
};

export default Header;
