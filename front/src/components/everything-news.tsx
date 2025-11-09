import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarTrigger,
} from "@/components/ui/menubar"
import { type EverythingFilter, Language, SortBy } from "../services/news-api/newsapi"
import { getEverythingNews } from "@/services/api";
import { Input } from "@/components/ui/input"
import React from "react";
import NewsList from "@/components/news-list"
import { Search } from "lucide-react"
import { Button } from "@/components/ui/button"


export const Filter: EverythingFilter = {
  domains: "bbc.co.uk, techcrunch.com, engadget.com",
  sortBy: SortBy.PUBLISHED_AT,
  language: Language.EN,
  pageSize: 20,
  page: 1
};

const defaultFilter: Pick<EverythingFilter, 'pageSize' | 'page'> = {
  pageSize: 20, 
  page: 1,       
};


export default function EverythingNews(){
  const [filters, setFilters] = React.useState<EverythingFilter>(Filter);
  const [q, setQ] = React.useState<string>("");

  const qHandler = () => {
    const Filter: EverythingFilter = {
      ...defaultFilter,
      ...filters,
      q: q,
    };
    setFilters(Filter);
  }

  return (
    <>
      <div className="mb-10">
        <p className="text-muted-foreground text-sm">
          Search through millions of articles from over 150,000 large and small news sources and blogs.
        </p>
      </div>
      <div className="flex">
      <Input 
        onChange={(e) => {setQ(e.target.value);}} 
        onKeyDown={(e) => {
          if(e.key === "Enter"){qHandler()}
        }}    
        className="mb-3 mr-3" placeholder="search" />
        <Button variant="outline" size="icon" onClick={qHandler}><Search/></Button>
      </div>
      <Menubar className="w-min">
        <MenubarMenu>
          <MenubarTrigger>
            {
              filters?.language? filters.language: "language"
            }
          </MenubarTrigger>
          <MenubarContent>
            {Object.values(Language).map((code, i) => (
              <MenubarItem onClick={() => {
                const Filter: EverythingFilter= {
                  ...defaultFilter,
                  ...filters,
                  language: code,
                };
                setFilters(Filter);
              }} key={i}>{code}</MenubarItem>
            ))}
          </MenubarContent>
        </MenubarMenu>
        <MenubarMenu>
          <MenubarTrigger>
            {filters?.sortBy? filters.sortBy: "sortBy"}
          </MenubarTrigger>
          <MenubarContent>
            {Object.values(SortBy).map((category, i)=> (
              <MenubarItem onClick={()=>{
                const Filter: EverythingFilter= {
                  ...defaultFilter,
                  ...filters,
                  sortBy: category,
                };
                setFilters(Filter);
              }} key={i}>{category}</MenubarItem>
            ))}
          </MenubarContent>
        </MenubarMenu>
      </Menubar>
      <NewsList filter={filters} setFilter={setFilters} getNews={getEverythingNews}/>
    </>
  )
}
