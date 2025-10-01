import LoginScreen from "@/components/login-screen";
import RegisterScreen from "@/components/register_screen";
import { Routes, Route } from "react-router-dom";


export default function Auth(){
  return (
    <div className="h-screen w-screen grid grid-cols-1 lg:grid-cols-2">
      <div className="bg-muted lg:block hidden">
      </div>
      <div className="">
        <Routes>
          <Route path="/sign_in" element={<LoginScreen />} />
          <Route path="/sign_up" element={<RegisterScreen />} />
        </Routes>
      </div>
    </div>
  )
}
