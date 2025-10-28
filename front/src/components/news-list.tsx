import { useEffect, useState } from "react"
import { getTopHeadlinesNews } from "../services/api.ts";
import { type NewsItem, type TopHeadlinesFilter } from "../services/news-api/newsapi";
import { Spinner } from "@/components/ui/spinner"
import NewsCard from "@/components/news-card"
import React from "react";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"



interface FilterProps {
  filter: TopHeadlinesFilter;      
  setFilter: React.Dispatch<React.SetStateAction<TopHeadlinesFilter>>;
}


const NewsList: React.FC<FilterProps> = ({filter, setFilter}) => {
  const [news, setNews] = useState<NewsItem[] | null>();
  const [countPages, setCountPages] = useState<number>(0);
  const countPagesInPagination = 5

  async function updateNews(){
    try {
      setNews(null);
      const res = await getTopHeadlinesNews(filter) ;
      if (res.data.data){
        const typedNews: NewsItem[] = res.data.data.news;
        setNews(typedNews);
        setCountPages(res.data.data.totalResults / filter.pageSize);
      }
    } catch (e) {
      console.log(e);
      console.error("Ошибка при получении новостей");
    }
  }

  useEffect(() => {
    updateNews();
  }, [filter]);

  if (!news){
    return (
      <div className="w-full h-[100vh] flex justify-center pt-[40vh]">
        <Spinner className="size-8"/> 
      </div>
    )
  }

  function getPaginatePages(i: number): number[]{
  }

  return (
    <>
      <div className="w-full flex flex-col">
        {news.map((value) => (
          <NewsCard news={value}/>
        ))}
      </div>
      <Pagination>
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious onClick={() => {setFilter({...filter, page: filter.page-1})}}/>
          </PaginationItem>
          {getPaginatePages(filter.page).map(i => (
            <PaginationItem>
              <PaginationLink href="#">{i}</PaginationLink>
            </PaginationItem>
          ))}
          <PaginationItem>
            <PaginationEllipsis />
          </PaginationItem>
          <PaginationItem>
            <PaginationNext onClick={() => {setFilter({...filter, page: filter.page+1})}} />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </>
  )
}

export default NewsList;
