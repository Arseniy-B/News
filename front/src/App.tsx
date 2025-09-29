import { ThemeProvider } from "@/components/theme-provider"
import { BrowserRouter, Routes, Route } from "react-router-dom";
// import { ModeToggle } from "@/components/mode-toggle"
import Signin from "@/pages/sign_in"
import Signup from "@/pages/sign_up"
import News from "@/pages/news"


function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <BrowserRouter>
        <Routes>
          <Route path="/signin" element={<Signin />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="*" element={<News />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
