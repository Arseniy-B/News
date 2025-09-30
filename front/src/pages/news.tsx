import { Routes, Route, Outlet } from "react-router-dom";
import { Button } from "@/components/ui/button"
import { getNews } from "../services/api.ts";


function PageNotFound(){
  return <>NotFound</>
}

export default function News() {
  async function clickHandler(){
    try {
      const res = await getNews({country: "US"});
      console.log("Новости:", res.data);
    } catch (e) {
      console.error("Ошибка при получении новостей");
    }
  }
  return (
    <>
      <Button onClick={clickHandler}>News</Button>
      <Routes>
        <Route path="/" />
        <Route path="*" element={<PageNotFound />}/>
      </Routes>
      <Outlet/>
    </>
  )
}
