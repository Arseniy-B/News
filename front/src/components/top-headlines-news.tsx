import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarSeparator,
  MenubarShortcut,
  MenubarTrigger,
} from "@/components/ui/menubar"
import { CountryCode, Category, type TopHeadlinesFilter } from "../services/news-api/newsapi"
import { getTopHeadlinesNews } from "../services/api";
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import React from "react";
import NewsList from "@/components/news-list"


const defaultFilter: Pick<TopHeadlinesFilter, 'pageSize' | 'page'> = {
  pageSize: 20, 
  page: 1,       
};

export default function TopHeadlinesNews(){
  const [filters, setFilters] = React.useState<TopHeadlinesFilter | null>(null);
  const [news, setNews] = React.useState(null);

  
  async function getNews(filters: TopHeadlinesFilter){
    await getTopHeadlinesNews(filters)
  }

  return (
    <>
      <Input onChange={(e) => {
        const Filter: TopHeadlinesFilter = {
          ...defaultFilter,
          ...filters,
          q: e.target.value,
        };
        setFilters(Filter);
      }} className="mb-3" placeholder="search" />
      <Menubar className="w-min">
        <MenubarMenu>
          <MenubarTrigger>
            {
              filters?.country? filters.country : "country"
            }
          </MenubarTrigger>
          <MenubarContent>
            {Object.values(CountryCode).map((code, i) => (
              <MenubarItem onClick={() => {
                const Filter: TopHeadlinesFilter = {
                  ...defaultFilter,
                  ...filters,
                  country: code,
                };
                setFilters(Filter);
              }} key={i}>{code}</MenubarItem>
            ))}
          </MenubarContent>
        </MenubarMenu>
        <MenubarMenu>
          <MenubarTrigger>
            {filters?.category? filters.category: "category"}
          </MenubarTrigger>
          <MenubarContent>
            {Object.values(Category).map((category, i)=> (
              <MenubarItem onClick={()=>{
                const Filter: TopHeadlinesFilter = {
                  ...defaultFilter,
                  ...filters,
                  category: category,
                };
                setFilters(Filter);
              }} key={i}>{category}</MenubarItem>
            ))}
          </MenubarContent>
        </MenubarMenu>
      </Menubar>
      <NewsList filter_data={filters}/>
    </>
  )
}
