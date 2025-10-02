import { Routes, Route } from "react-router-dom";
import HeaderMenu from "@/components/header-menu";
import NewsList from "@/components/news-list";


function PageNotFound(){
  return <>NotFound</>
}

export default function News() {
  return (
    <>
      <div className="flex justify-end">
        <HeaderMenu />
      </div>
      <div>
        <NewsList />
      </div>
      <Routes>
        <Route path="/" />
        <Route path="*" element={<PageNotFound />}/>
      </Routes>
    </>
  )
}
