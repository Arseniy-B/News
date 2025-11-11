import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarTrigger,
} from "@/components/ui/menubar"
import { CountryCode, Category, type TopHeadlinesFilter, Filter } from "../services/news-api/newsapi"
import { Input } from "@/components/ui/input"
import React from "react";
import NewsList from "@/components/news-list"
import { getTopHeadlinesNews, getUserFilters } from "@/services/api";
import { Search } from "lucide-react"
import { Button } from "@/components/ui/button"


const defaultFilter: Pick<TopHeadlinesFilter, 'pageSize' | 'page'> = {
  pageSize: 20, 
  page: 1,       
};

export default function TopHeadlinesNews(){
  const [filters, setFilters] = React.useState<TopHeadlinesFilter>(Filter);
  const [q, setQ] = React.useState<string>("");

  const qHandler = () => {
    const Filter: TopHeadlinesFilter = {
      ...defaultFilter,
      ...filters,
      q: q,
    };
    setFilters(Filter);
  }

  // async function getFilters(){
  //   const res = await getUserFilters();
  //   console.log(res);
  // }
  // React.useEffect(() => {
  //   getFilters()
  // }, [])

  return (
    <>
      <div className="mb-10">
        <p className="text-muted-foreground text-sm">
        This endpoint provides live top and breaking headlines for a country, specific category in a country, single source, or multiple sources. You can also search with keywords. Articles are sorted by the earliest date published first.
        </p>
      </div>
      <div className="flex">
        <Input 
          onChange={(e) => {setQ(e.target.value);}} 
          onKeyDown={(e) => {
            if (e.key === "Enter"){qHandler()}
          }} 
          className="mb-3 mr-3" 
          placeholder="search" 
        />
        <Button variant="outline" size="icon" onClick={qHandler}><Search/></Button>
      </div>
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
      <NewsList filter={filters} setFilter={setFilters} getNews={getTopHeadlinesNews}/>
    </>
  )
}
