import {
  Card,
} from "@/components/ui/card"
import type { NewsItem } from "../services/news-api/newsapi";
import React from "react";
import { Badge } from "@/components/ui/badge"
import { ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"


interface NewsCardProps {
  news: NewsItem;
}


export default function NewsCard({ news }: NewsCardProps){
  const [passedTime, setPassedTime] = React.useState<string>("");

  React.useEffect(() => {
    const pastDate = new Date(news.publishedAt);
    const now = new Date();

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
            className={'w-full transition-opacity duration-300 opacity-100 h-0'}
            loading="lazy"  
            onLoad={(e) => {
              const img = e.target as HTMLImageElement;
              img.style.height = "calc(var(--spacing) * 48)"
            }}
          />
        </div>
        <div className="flex flex-col content-between p-[8%]">
          <div className="mb-10">
            <h4 className="scroll-m-20 text-xl font-semibold tracking-tight">{news.title}</h4>
            <p className="leading-7 [&:not(:first-child)]:mt-6">{news.content}</p>
            <p className="leading-7 [&:not(:first-child)]:mt-6">{news.description}</p>
          </div>
          <div className="flex justify-between">
            <div>
              <Tooltip>
                <TooltipTrigger>
                  <Badge className="m-1" variant="default">published {passedTime} ago</Badge>
                </TooltipTrigger>
                <TooltipContent>time after publication</TooltipContent>
              </Tooltip>
              <Tooltip>
                <TooltipTrigger>
                  <Badge className="m-1" variant="secondary">{news.author}</Badge>
                </TooltipTrigger>
                <TooltipContent>author</TooltipContent>
              </Tooltip>
              <Tooltip>
                <TooltipTrigger>
                  <Badge className="m-1" variant="destructive">{news.source.name}</Badge>
                </TooltipTrigger>
                <TooltipContent>source</TooltipContent>
              </Tooltip>
            </div>
            <div>
              {news.url &&
                <Button 
                   onClick={() => {if(news.url){window.open(news.url, '_blank', 'noopener,noreferrer')}}} variant="ghost" size="icon"
                >
                  <ExternalLink/>
                </Button>
              }
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}
