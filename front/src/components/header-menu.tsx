import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import { Button } from "@/components/ui/button";
import { Logs } from "lucide-react";
import { ModeToggle } from "@/components/mode-toggle"
import { filterService, Filter, Category, CountryCode } from "../services/news-api/newsapi";


export default function HeaderMenu(){
  const oldFilters = filterService.get();
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="ghost"><Logs/></Button>
      </SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>Theme</SheetTitle>
          <SheetDescription>
            <ModeToggle />
          </SheetDescription>
          <SheetTitle>Filters</SheetTitle>
          <SheetDescription className="flex gap-3 flex-col">
            <Select onValueChange={(value) => {
              let filters = Filter;
              const storageFilters = filterService.get();
              if (storageFilters){
                filters = storageFilters;
              }
              filters.country = Object.values(CountryCode).includes(value as any) ? value as CountryCode : null;
              filterService.set(filters)
            }}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder={oldFilters? oldFilters.country : "Country"} />
              </SelectTrigger>
              <SelectContent>
                {Object.values(CountryCode).map(value => (
                  <SelectItem value={value}>{value}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select onValueChange={(value) => {
              let filters = Filter;
              const storageFilters = filterService.get();
              if (storageFilters){
                filters = storageFilters;
              }
              filters.category = Object.values(Category).includes(value as any) ? value as Category: null;
              filterService.set(filters)
            }}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder={oldFilters? oldFilters.category : "Category"} />
              </SelectTrigger>
              <SelectContent>
                {Object.values(Category).map(value => (
                  <SelectItem value={value}>{value}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </SheetDescription>
        </SheetHeader>
      </SheetContent>
    </Sheet>
  )
}
