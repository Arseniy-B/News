import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";


export type Source = {
  id?: string;
  name?: string;
}

export type NewsItem = {
  source: Source;
  author?: string | null;
  title: string;
  description?: string | null;
  url?: string | null;
  urlToImage?: string | null;
  publishedAt: Date; 
  content?: string | null;
}

type Status = 'ok' | 'error';

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
