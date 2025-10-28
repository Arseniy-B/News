import {
  Card,
  CardContent,
} from "@/components/ui/card"
import type { NewsItem } from "../services/news-api/newsapi";
import React from "react";


interface NewsCardProps {
  news: NewsItem;
}


export default function NewsCard({ news }: NewsCardProps){
  const [passedTime, setPassedTime] = React.useState<string>("");

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
      <Card className="m-auto p-[10%]">
        <h4 className="scroll-m-20 text-xl font-semibold tracking-tight">{news.title}</h4>
        <p className="leading-7 [&:not(:first-child)]:mt-6">{news.content}</p>
        <p className="leading-7 [&:not(:first-child)]:mt-6">{news.description}</p>
        <div>published {passedTime} ago</div>
        <div>{news.author}</div>
      </Card>
    </div>
  )
}
