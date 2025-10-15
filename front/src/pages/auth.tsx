import LoginScreen from "@/components/login-screen";
import RegisterScreen from "@/components/register-screen";
import { Routes, Route } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { useNavigate } from 'react-router-dom';


function NotFound(){
  return (
    <div className="w-full h-full flex justify-center items-center"><h1 className="text-[50px]">Not found</h1></div>
  )
}

export default function Auth(){
  const navigate = useNavigate();
  return (
    <div className="h-screen w-screen grid grid-cols-1 lg:grid-cols-2">
      <div className="bg-muted lg:block hidden">
        <Button className="m-10" onClick={() => {navigate("/news")}}>News</Button> 
      </div>
      <div>
        <Routes>
          <Route path="/sign_in" element={<LoginScreen />} />
          <Route path="/sign_up" element={<RegisterScreen />} />
          <Route path="*" element={<NotFound/>} />
        </Routes>
      </div>
    </div>
  )
}
