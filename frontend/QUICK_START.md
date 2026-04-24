# VitalTriage Frontend - Quick Start

## ⚡ 30 Seconds to Running

```bash
# 1. Install dependencies
npm install

# 2. Copy environment config
cp .env.example .env

# 3. Start development server
npm run dev
```

That's it! Open **http://localhost:5173** in your browser.

## ✅ Prerequisites

- Node.js 16+
- Backend API running at `http://localhost:8000`

## 🎯 What You'll See

A hospital dashboard with:
- 4 columns (Critical, High, Moderate, Stable patients)
- Real-time patient cards with vitals
- Alert banner for critical patients
- Add/Update patient buttons

## 📝 Environment Setup

Create `.env` file:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=10000
```

## 🔨 Common Commands

```bash
# Development with hot reload
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview

# Lint code (after installing eslint packages)
npm run lint
```

## 📁 Key Files to Know

- `src/pages/DashboardPage.tsx` - Main dashboard
- `src/components/Dashboard/Dashboard.tsx` - Patient grid
- `src/services/api.ts` - API integration
- `src/store/useStore.ts` - Global state

## 🆘 Troubleshooting

### Frontend won't load?
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Can't connect to API?
1. Verify backend is running on `http://localhost:8000`
2. Check CORS is enabled on backend
3. Update `VITE_API_BASE_URL` in `.env` if needed

### Hot reload not working?
```bash
# Restart dev server
npm run dev
```

## 🚀 Next Steps

1. **Explore Components**: Check `src/components/`
2. **Review Types**: See `src/types/patient.ts`
3. **Check Styling**: Tailwind CSS in `tailwind.config.ts`
4. **Test API**: Make requests in `src/services/api.ts`

## 📚 Full Documentation

See `FRONTEND_SETUP.md` for complete setup guide and architecture details.

## 🎨 Technology Stack

- React 18
- TypeScript
- Tailwind CSS
- React Query
- Zustand
- Axios
- Vite

## 💡 Tips

1. **Auto-refresh**: Dashboard updates every 5 seconds automatically
2. **Type Safety**: Full TypeScript support
3. **Hot Reload**: Changes reflect instantly during development
4. **DevTools**: Use React DevTools browser extension for debugging

---

Happy coding! 🎉
