export const Footer = () => {
  return (
    <footer className="bg-slate-900 text-slate-200 py-8 border-t border-slate-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="font-semibold text-white mb-2">VitalTriage</h3>
            <p className="text-sm text-slate-400">
              Hospital-grade real-time patient monitoring system
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-white mb-2">Quick Links</h3>
            <ul className="text-sm space-y-1 text-slate-400">
              <li><a href="#" className="hover:text-white transition">Dashboard</a></li>
              <li><a href="#" className="hover:text-white transition">Documentation</a></li>
              <li><a href="#" className="hover:text-white transition">Support</a></li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold text-white mb-2">Status</h3>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-slate-400">System Online</span>
            </div>
          </div>
        </div>
        <div className="border-t border-slate-700 pt-8 text-center text-sm text-slate-400">
          <p>&copy; 2024 VitalTriage. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
