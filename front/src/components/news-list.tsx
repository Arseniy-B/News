import { useEffect, useState } from "react"
import { getNews } from "../services/api.ts";
import type { AxiosResponse } from 'axios';
import type { NewsResponse, NewsItem } from "@/components/news-card";


export default function NewsList(){
  const [news, setNews] = useState<NewsItem[] | null>();

  async function addNews(){
    try {
      const res = await getNews({country: "US"}) as AxiosResponse<NewsResponse>;
      console.log(res);
      const typedNews: NewsItem[] = res.data.news;
      setNews(typedNews);
      console.log(news);
      console.log("Новости:", res.data);
    } catch (e) {
      console.error("Ошибка при получении новостей");
    }
  }
  useEffect(() => {addNews()}, []);

  return (
    <></>
  )
}
