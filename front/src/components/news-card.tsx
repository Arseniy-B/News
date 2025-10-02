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


export interface Source {
  id?: string;
  name?: string;
}

export interface NewsItem {
  source: Source;
  author?: string;
  title: string;
  description?: string;
  url?: string;
  urlToImage?: string;
  publishedAt: Date; 
  content?: string;
}

type Status = 'ok' | 'error';

export interface NewsResponse {
  news: NewsItem[];
  status: Status;
  totalResults: number;
}

export default function NewsCard({source, author, title, description, url, urlToImage, publishedAt, content}: NewsItem){
  const formattedDate = publishedAt.toLocaleDateString("ru-RU", { 
    year: "numeric", 
    month: "long", 
    day: "numeric" 
  });

  return (
    <Card className="w-full max-w-sm overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300">
      {urlToImage && (
        <CardHeader className="p-0">
        </CardHeader>
      )}
      <CardContent className="p-4 space-y-3">
        <div className="flex items-center justify-between">
          {source.name && (
            <Badge variant="secondary" className="text-xs">{source.name}</Badge>
          )}
          <span className="text-xs text-gray-500">{formattedDate}</span>
        </div>
        {author && (
          <div className="text-sm text-gray-600 italic">Автор: {author}</div>
        )}
        <CardTitle className="text-lg font-bold line-clamp-2">{title}</CardTitle>
        {(description || content) && (
          <CardDescription className="text-sm text-gray-600 line-clamp-3">
            {description || content}
          </CardDescription>
        )}
      </CardContent>
      {url && (
        <CardFooter className="p-4 pt-0">
          <Button asChild variant="outline" className="w-full">
          </Button>
        </CardFooter>
      )}
    </Card>
  )
}
