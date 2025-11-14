import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarTrigger,
} from "@/components/ui/menubar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { type EverythingFilter, Language, SortBy, Domains, SearchIn, DefaultEverythingFIlter } from "../services/news-api/newsapi"
import { getEverythingNews } from "@/services/api";
import { Input } from "@/components/ui/input"
import React from "react";
import NewsList from "@/components/news-list"
import { Search, SwatchBook } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Tooltip,
  TooltipProvider,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"


const defaultFilter: Pick<EverythingFilter, 'pageSize' | 'page'> = {
  pageSize: 20, 
  page: 1,       
};


export default function EverythingNews(){
  const [filters, setFilters] = React.useState<EverythingFilter>(DefaultEverythingFIlter);
  const [q, setQ] = React.useState<string>("");
  const [currentSearchIn, setCurrentSearchIn] = React.useState<SearchIn[]>(DefaultEverythingFIlter.searchIn);
  const [currentDomains, setCurrentDomains] = React.useState<Domains[]>(DefaultEverythingFIlter.domains);

  const qHandler = () => {
    const Filter: EverythingFilter = {
      ...defaultFilter,
      ...filters,
      q: q,
      searchIn: currentSearchIn,
      domains: currentDomains
    };
    if (!q){
      Filter.q = undefined
    }
    setFilters(Filter);
  }

  const changeSearchIn = (field: SearchIn) => {
    var searchIn
    if (currentSearchIn.includes(field)){
      searchIn = currentSearchIn.filter(item => item !== field)
    } else {
      searchIn = [...currentSearchIn, field]
    }
    if (searchIn.length === 0){
      searchIn = [SearchIn.TITLE]
    }
    setCurrentSearchIn(searchIn);
  }

  const changeDomains = (field: Domains) => {
    var domains;
    if (currentDomains.includes(field)){
      domains = currentDomains.filter(item => item !== field)
    } else {
      domains = [...currentDomains, field]
    }
    if (domains.length === 0){
      domains = [Domains.BBC, Domains.ECHCRUNCH, Domains.ENGADGET]
    }
    setCurrentDomains(domains);
    console.log(domains);
  }

  return (
    <>
      <div className="mb-10">
        <p className="text-muted-foreground text-sm">
          Search through millions of articles from over 150,000 large and small news sources and blogs.
        </p>
      </div>
      <div className="flex gap-1">
        <Input 
          onChange={(e) => {setQ(e.target.value);}} 
          onKeyDown={(e) => {if(e.key === "Enter"){qHandler()}}}
          className="mb-3" placeholder="search" 
        />
        <Button variant="outline" size="icon" onClick={qHandler}><Search/></Button>
        
        <TooltipProvider>
          <Popover>
            <Tooltip>
              <TooltipTrigger asChild>
                <PopoverTrigger asChild>
                  <Button variant="ghost" size="icon"><SwatchBook/></Button>
                </PopoverTrigger>
              </TooltipTrigger>
              <TooltipContent>
                <p className="leading-7 [&:not(:first-child)]:mt-6">
                  Search settings
                </p>
              </TooltipContent>
            </Tooltip>
            <PopoverContent className="w-min flex">
              <div>
                <p>Domains</p>
                <Button onClick={() => {
                  changeDomains(Domains.BBC);
                }} variant={currentDomains.includes(Domains.BBC) ? "secondary" : "ghost"}>BBC</Button>
                <Button onClick={() => {
                  changeDomains(Domains.ENGADGET);
                }} variant={currentDomains.includes(Domains.ENGADGET) ? "secondary" : "ghost"}>Engadget</Button>
                <Button onClick={() => {
                  changeDomains(Domains.ECHCRUNCH);
                }} variant={currentDomains.includes(Domains.ECHCRUNCH) ? "secondary" : "ghost"}>Echcrunch</Button>
              </div>

              <div className="flex flex-col">
                <p>Search in</p>
                <Button onClick={() => {
                  changeSearchIn(SearchIn.TITLE);
                }} variant={currentSearchIn.includes(SearchIn.TITLE) ? "secondary" : "ghost"}>Title</Button>
                <Button onClick={() => {
                  changeSearchIn(SearchIn.CONTENT);
                }} variant={currentSearchIn.includes(SearchIn.CONTENT) ? "secondary" : "ghost"}>content</Button>
                <Button onClick={() => {
                  changeSearchIn(SearchIn.DESCRIPTION);
                }} variant={currentSearchIn.includes(SearchIn.DESCRIPTION) ? "secondary" : "ghost"}>description</Button>
              </div>
            </PopoverContent>
          </Popover>
        </TooltipProvider>
          
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
