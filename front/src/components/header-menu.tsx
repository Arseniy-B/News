import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"

import { Logs } from "lucide-react";
import { ModeToggle } from "@/components/mode-toggle"


export default function HeaderMenu(){
  return (
    <Sheet>
      <SheetTrigger className="m-2">
        <Logs/>
      </SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>Theme</SheetTitle>
          <SheetDescription>
            <ModeToggle />
          </SheetDescription>
        </SheetHeader>
      </SheetContent>
    </Sheet>
  )
}
