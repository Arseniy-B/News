import { Routes, Route, Outlet } from "react-router-dom";


function PageNotFound(){
  return <>NotFound</>
}

export default function News() {
  return (
    <>
      News
      <Routes>
        <Route path="*" element={<PageNotFound />}/>
      </Routes>
      <Outlet/>
    </>
  )
}
