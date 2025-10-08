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


export default function HeaderMenu(){
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
            
          </SheetDescription>
        </SheetHeader>
      </SheetContent>
    </Sheet>
  )
}
