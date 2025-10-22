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
import ChoiceFilters from "@/components/choice-filters" 
import { type BaseFilter } from "../services/news-api/newsapi";
import React from "react";


export default function HeaderMenu(){
  const [currentFilter, setCurrentFilter] = React.useState<BaseFilter | null>(null);
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
          <SheetDescription>
            <ChoiceFilters currentFilter={currentFilter} setCurrentFilter={setCurrentFilter}/>
          </SheetDescription>
        </SheetHeader>
      </SheetContent>
    </Sheet>
  )
}
