import { useEffect, useState } from "react"
import { getNews } from "../services/api.ts";
import { Filter, type NewsItem } from "../services/news-api/newsapi";
import { Spinner } from "@/components/ui/spinner"
import {
  type CarouselApi,
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"
import NewsCard from "@/components/news-card"




export default function NewsList(filter_data: Record<string, any>){
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
      const filters = filter_data;
      const res = await getNews(filters? filters : Filter) ;
      const typedNews: NewsItem[] = res.data.data;
      setNews(typedNews);
    } catch (e) {
      console.log(e);
      console.error("Ошибка при получении новостей");
    }
  }

  useEffect(() => { 
    if(current === 10){
      addNews()
    }
  }, [current])

  useEffect(() => {
    if (news){
      setCarousels(carousels => carousels ? [...carousels, news] : [news]);
    }
  }, [news]);

  useEffect(() => {
    addNews()
  }, []);


  if (!news || !carousels){
    return (
      <div className="w-full h-[100vh] flex justify-center pt-[40vh]">
        <Spinner className="size-8"/> 
      </div>
    )
  }

  return (
    <div className="w-100 mx-auto">
      {carousels.map((item, index) => (
        <div key={index} data-carousel-index={index} className="h-[100vh] py-50">
          <Carousel setApi={setApi}>
            <CarouselContent>
              {item.map((n, index) => (
                <CarouselItem key={index}>
                  <NewsCard news={n} />
                </CarouselItem>
              ))}
              <CarouselItem>space</CarouselItem>
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>
      ))}
    </div>
  )
}
