import { useEffect, useState } from "react"
import { type Response } from "../services/api.ts";
import { type NewsItem, type BaseFilter } from "../services/news-api/newsapi";
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
import { type AxiosResponse } from "axios";


interface FilterProps<T extends BaseFilter> {
  filter: T;      
  setFilter: React.Dispatch<React.SetStateAction<T>>;
  getNews: (news: T) => Promise<AxiosResponse<Response<{news: NewsItem[], totalResults: number}>>>
}


const NewsList = <T extends BaseFilter>({
  filter,
  setFilter,
  getNews
}: FilterProps<T>): React.JSX.Element => {
  const [news, setNews] = useState<NewsItem[] | null>();
  const [countPages, setCountPages] = useState<number>(0);
  const countPagesInPagination = 5

  async function updateNews(){
    try {
      setNews(null);
      const res = await getNews(filter);
      if (res.data.data){
        const typedNews: NewsItem[] = res.data.data.news;
        setNews(typedNews);
        setCountPages(Math.ceil(res.data.data.totalResults / filter.pageSize));
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
    console.log(i, countPages, countPagesInPagination);
    function range(a: number, b: number): number[]{
      console.log(a, b);
      return [...Array(b - a + 1).keys()].map(i => i + a)
    }
    if(countPagesInPagination <= 0 || countPages <= 0){
      return []
    }
    if(countPages <= countPagesInPagination){
      return range(1, countPages);
    }
    
    var r = i + (countPagesInPagination - (Math.floor(countPagesInPagination / 2)));
    var l = i - (Math.floor(countPagesInPagination / 2));

    if(r > countPages){
      r = countPages;
      l -= r - countPages + 1;
    }

    if(l < 1){
      if(r >= countPages){
        return range(1, countPages);
      }
      l = 1;
      r = countPagesInPagination
    }
    return range(l, r)
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
              <PaginationLink 
                className={filter.page === i ? 'bg-chart-3' : ''}
                onClick={() => {setFilter({...filter, page: i})}}
              >
                {i}
              </PaginationLink>
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
