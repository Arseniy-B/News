import {
  Card,
} from "@/components/ui/card"
import type { NewsItem } from "../services/news-api/newsapi";
import React from "react";
import { Badge } from "@/components/ui/badge"


interface NewsCardProps {
  news: NewsItem;
}


export default function NewsCard({ news }: NewsCardProps){
  const [passedTime, setPassedTime] = React.useState<string>("");
  const [isLoaded, setIsLoaded] = React.useState<boolean>(false);

  React.useEffect(() => {
    const pastDate = new Date(news.publishedAt);
    const now = new Date(); // Текущее время в браузере

    const diffMs = now.getTime() - pastDate.getTime();

    const seconds = Math.floor(diffMs / 1000);
    const minutes = Math.floor(diffMs / (1000 * 60));
    const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if(seconds < 60){
      setPassedTime(`${seconds} seconds`);
    } else if (minutes < 60){
      setPassedTime(`${minutes} minutes`);
    } else if (days < 7) {
      setPassedTime(`${days} days`);
    } else if (days < 30){
      setPassedTime("more than a month");
    }
  }, [])

  return (
    <div className="w-full min-h-[90vh] p-[5%] content-center">
      <Card className="m-auto p-[2%]">
        <div>
          <img
            src={news.urlToImage? news.urlToImage: ""}
            className={`w-full h-48 transition-opacity duration-300 ${
              isLoaded ? 'opacity-100' : 'opacity-0'
            }`}
            loading="lazy"  // Lazy loading для производительности
            onLoad={() => setIsLoaded(true)}  // Скрыть skeleton при загрузке
            onError={() => setIsLoaded(true)}  // На ошибку тоже скрыть (показать пустой)
          />
        </div>
        <div className="flex flex-col content-between p-[8%]">
          <div className="mb-10">
            <h4 className="scroll-m-20 text-xl font-semibold tracking-tight">{news.title}</h4>
            <p className="leading-7 [&:not(:first-child)]:mt-6">{news.content}</p>
            <p className="leading-7 [&:not(:first-child)]:mt-6">{news.description}</p>
          </div>
          <div>
            <Badge variant="default">published {passedTime} ago</Badge>
            <Badge variant="secondary">{news.author}</Badge>
          </div>
        </div>
      </Card>
    </div>
  )
}
