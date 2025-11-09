import { Routes, Route, useLocation } from "react-router-dom";
import AuthMenu from "@/components/auth-menu";
import EverythingNews from "@/components/everything-news";
import TopHeadlinesNews from "@/components/top-headlines-news";
import { Navigate } from 'react-router-dom';
import { Link } from "react-router-dom"
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu"
import { ModeToggle } from "@/components/mode-toggle";


function PageNotFound(){
  return <>NotFound</>
}


export default function News() {
  const location = useLocation();  
  const currentPath = location.pathname;
  const currentMode = currentPath.includes('everything') ? 'Everything' : 'Top Headlines';  

  return (
    <>
      <div className="flex justify-end fixed gap-2 p-2 w-full z-50 bg-background">
        <NavigationMenu>
          <NavigationMenuList>
            <NavigationMenuItem>
              <NavigationMenuTrigger>{currentMode}</NavigationMenuTrigger>
              <NavigationMenuContent>
                <NavigationMenuLink asChild>
                  <Link to="/news/everything">Everything</Link>
                </NavigationMenuLink>
                <NavigationMenuLink asChild>
                  <Link to="/news/top-headlines">TopHeadlines</Link>
                </NavigationMenuLink>
              </NavigationMenuContent>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <AuthMenu />
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NavigationMenuLink asChild>
                <ModeToggle />
              </NavigationMenuLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
      </div>
      <div className="flex flex-col justify-end py-20 px-[10vw]">
        <Routes>
          <Route path="/" element={<Navigate to="/news/everything" replace />} />
          <Route path="everything" element={<EverythingNews />} />
          <Route path="top-headlines" element={<TopHeadlinesNews />} />
          <Route path="*" element={<PageNotFound />}/>
        </Routes>
      </div>
    </>
  )
}
