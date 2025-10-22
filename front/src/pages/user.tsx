import Profile from "@/pages/profile";
import { Routes, Route } from "react-router-dom";


function NotFound(){
  return (
    <div className="w-full h-full flex justify-center items-center"><h1 className="text-[50px]">Not found</h1></div>
  )
}

export default function User(){
  return (
    <>
      <Routes>
        <Route path="/profile" element={<Profile />} />
        <Route path="*" element={<NotFound/>} />
      </Routes>
    </>
  )
}
