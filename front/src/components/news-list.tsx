import { useEffect, useState } from "react"
import { getNews } from "../services/api.ts";
import type { AxiosResponse } from 'axios';
import type { NewsResponse, NewsItem } from "@/components/news-card";

import {
  type CarouselApi,
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"

import NewsCard from "@/components/news-card"


export default function NewsList(){
  const [news, setNews] = useState<NewsItem[] | null>();
  const [carousels, setCarousels] = useState<NewsItem[][] | null>();
  const [api, setApi] = useState<CarouselApi>();
  const [current, setCurrent] = useState(0);


  useEffect(() => {
    if (!api) return;
    setCurrent(api.selectedScrollSnap());  
    api.on("select", () => {
      setCurrent(api.selectedScrollSnap());
    });
  }, [api]);

  async function addNews(){
    try {
      const res = await getNews({country: "US"}) as AxiosResponse<NewsResponse>;
      const typedNews: NewsItem[] = res.data.news;
      setNews(typedNews);
    } catch (e) {
      console.error("Ошибка при получении новостей");
    }
  }

  useEffect(() => { 
    if(current === 16){
      addNews()
    }
  }, [current])


  useEffect(() => {addNews()}, []);

  useEffect(() => {
    console.log(news);
    if (news){
      setCarousels(carousels => carousels ? [...carousels, news] : [news]);
    }
  }, [news]);

  useEffect(() => {
    if (carousels) {
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }
  }, [carousels]);

  if (!news){
    return <div className="w-100 mx-auto">Load</div>
  }
  if (!carousels){
    return <div></div>
  }

  return (
    <div className="w-100 mx-auto">
      {carousels.map((item) => (
        <Carousel setApi={setApi}>
          <CarouselContent>
            {item.map((n, index) => (
              <CarouselItem key={index}>
                <NewsCard news={n} />
              </CarouselItem>
            ))}
            <CarouselItem>
            </CarouselItem>
          </CarouselContent>
          <CarouselPrevious />
          <CarouselNext />
        </Carousel>
      ))}
      <div className="h-50"></div>
    </div>
  )
}
