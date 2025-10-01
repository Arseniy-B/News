import { ThemeProvider } from "@/components/theme-provider"
import { BrowserRouter, Routes, Route } from "react-router-dom";
// import { ModeToggle } from "@/components/mode-toggle"
import { Navigate } from 'react-router-dom';
import Auth from "@/pages/auth"
import News from "@/pages/news"


function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <BrowserRouter>
        <Routes>
          <Route path="/auth/*" element={<Auth />} />
          <Route path="/news/*" element={<News />} />
          <Route path="*" element={<Navigate to="/news" replace />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
