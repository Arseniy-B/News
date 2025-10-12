import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card"
import type { NewsItem } from "../services/news-api/newsapi";


interface NewsCardProps {
  news: NewsItem;
}

export type NewsResponse = NewsItem[]


export default function NewsCard({ news }: NewsCardProps){
  return (
    <Card>
      <CardHeader>
        {news.urlToImage && <img src={news.urlToImage} alt="Описание" />}
        {news.title}
      </CardHeader>
      <CardContent>{news.description}</CardContent>
      <CardFooter></CardFooter>
    </Card>
  )
}
