import { Routes, Route } from "react-router-dom";
import HeaderMenu from "@/components/header-menu";
import NewsList from "@/components/news-list";
import AuthMenu from "@/components/auth-menu";


function PageNotFound(){
  return <>NotFound</>
}

export default function News() {
  return (
    <>
      <div className="flex justify-end fixed gap-2 p-2 w-full z-50 bg-background">
        <AuthMenu />
        <HeaderMenu />
      </div>
      <div className="flex flex-col justify-end">
        <NewsList />
      </div>
      <Routes>
        <Route path="/" />
        <Route path="*" element={<PageNotFound />}/>
      </Routes>
    </>
  )
}
