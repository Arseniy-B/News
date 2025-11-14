import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Card,
  CardContent,
  CardFooter,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useNavigate } from 'react-router-dom';
import { getUser, refreshToken, logout, tokenService, getUserFilters, setUserFilters } from "../services/api";
import { useEffect, useState } from "react";
import type { User } from "../services/user-api";
import { format } from 'date-fns';
import type { TopHeadlinesFilter, EverythingFilter } from '../services/news-api/newsapi';
import { CountryCode, Category, Filter, DefaultEverythingFIlter, SortBy, Language, Domains } from '../services/news-api/newsapi';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { AxiosError } from "axios";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"


export default function Profile(){
  const [topHeadlines, setTopHeadlines] = useState<TopHeadlinesFilter>(Filter);
  const [everything, setEverything] = useState<EverythingFilter>(DefaultEverythingFIlter);
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null); 
  const [isImpacted, setIsImpacted] = useState(false);


  const handleClick = () => {
    setIsImpacted(true);
    setTimeout(() => setIsImpacted(false), 1000);
  };

  async function getUserData(){
    var res = null;
    try{
    res = await getUser();
    } catch (e) {
      if(e instanceof AxiosError){
        try{
          await refreshToken();
          res = await getUser();
        }catch(e){
          navigate("/auth/sign_in/");
        }
      }
    }
    if(res){
      setUser(res.data.data);
    }
  }

  async function getFilters(){
    var res = await getUserFilters(["Everything", "TopHeadlines"]);
    if (res.data.data){
      for(var i = 0; i < res.data.data.length; i++){
        const filter = res.data.data[i]
        switch (filter.filter_type){
          case "TopHeadlines":
            setTopHeadlines(filter);
            break;
          case "Everything":
            setEverything(filter);
            break
        }
      }
    }
  }
  useEffect(() => {
    getUserData();
    getFilters();
  }, [])

  async function setTopHeadlinesFilters(){
    await setUserFilters(topHeadlines, topHeadlines.filter_type);
  }
  async function setEverythingFilters(){
    await setUserFilters(everything, everything.filter_type) 
  }

  async function logoutHandler(){
    await logout();
    tokenService.delete();
    navigate("/auth/sign_in");
  }

  const toggleDomain = (domain: Domains) => {
    const new_domains = everything.domains.includes(domain) 
      ? everything.domains.filter(d => d !== domain) 
      : [...everything.domains, domain];
    setEverything({...everything, domains: new_domains});
  };

  return (
    <>
      <div className="fixed w-full p-5 flex justify-end">
        <AlertDialog>
          <AlertDialogTrigger asChild>
            <Button variant="destructive">Log out</Button>
          </AlertDialogTrigger>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
              <AlertDialogDescription>
                Do you want to log out of your account?
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction onClick={logoutHandler} className="bg-destructive">Continue</AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
        <Button variant="ghost" onClick={() => navigate("/news")}>News</Button>
      </div>
      <div className="h-[100vh] grid lg:grid-cols-7">
        <div className="col-span-4 lg:col-span-3 pl-[10vw] bg-secondary flex flex-col font-thin text-[15px]">
          <div className="h-[30vh]"></div>
          <div>username: <div className="font-light text-[20px] mb-5">{user?.username}</div></div>
          <div>email: <div className="font-light text-[20px] mb-5">{user?.email}</div></div>
          <div>created at: <div className="font-light text-[20px] mb-5">{user?.created_at ? format(user.created_at, 'yyyy-MM-dd HH:mm') : 'N/A'}</div></div>
        </div>
        <div className="col-span-4">
          <Card className="w-full h-full rounded-[0] bg-background">
            <CardContent>
              <div className="text-[30px] font-thin flex flex-col">Settings</div>
                <Tabs>
                  <TabsList>
                    <TabsTrigger value="Everything">Everything</TabsTrigger>
                    <TabsTrigger value="TopHeadlines">TopHeadlines</TabsTrigger>
                  </TabsList>

                  <TabsContent value="Everything">
                    <Select onValueChange={(value: SortBy) => {
                      setEverything({...DefaultEverythingFIlter, ...everything, sortBy: value})    
                    }}>
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder={everything.sortBy} />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.values(SortBy).map((sortBy) => (
                          <SelectItem value={sortBy}>{sortBy}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Select onValueChange={(value: Language) => {
                      setEverything({...DefaultEverythingFIlter, ...everything, language: value})    
                    }}>
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder={everything.language} />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.values(Language).map((language) => (
                          <SelectItem value={language}>{language}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <div>
                      <div className="flex items-center space-x-2">
                        <Switch defaultChecked={everything.domains.includes(Domains.BBC)} onCheckedChange={() => {
                          toggleDomain(Domains.BBC);
                        }} id="BBC" />
                        <Label htmlFor="BBC">BBC</Label>

                        <Switch defaultChecked={everything.domains.includes(Domains.ENGADGET)} onCheckedChange={() => {
                          toggleDomain(Domains.ENGADGET);
                        }} id="ENGADGET" />
                        <Label htmlFor="ENGADGET">Engadget</Label>

                        <Switch defaultChecked={everything.domains.includes(Domains.ECHCRUNCH)} onCheckedChange={() => {
                          toggleDomain(Domains.ECHCRUNCH);
                        }} id="ECHCRUNCH" />
                        <Label htmlFor="ECHCRUNCH">Echcrunch</Label>
                      </div>
                    </div>
                    <Button
                      onClick={() => {
                        if(!isImpacted){
                          setEverythingFilters();
                          handleClick();
                        }
                      }}
                      className={`transition-transform duration-150 ${
                      isImpacted ? "scale-95 opacity-80" : ""
                    }`}>
                      submit
                    </Button>
                    <Button variant="ghost" onClick={() => {
                      setEverything(DefaultEverythingFIlter);
                    }}>reset default</Button>
                  </TabsContent>

                  <TabsContent value="TopHeadlines">
                    <Select onValueChange={(value: CountryCode) => {
                      setTopHeadlines({...Filter, ...topHeadlines, country: value})    
                    }}>
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder={topHeadlines.country} />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.values(CountryCode).map((code) => (
                          <SelectItem value={code}>{code}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Select onValueChange={(value: Category) => {
                      setTopHeadlines({...Filter, ...topHeadlines, category: value})    
                    }}>
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder={topHeadlines.category? topHeadlines.category : "category"} />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.values(Category).map((category) => (
                          <SelectItem value={category}>{category}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Button
                      onClick={() => {
                        if(!isImpacted){
                          setTopHeadlinesFilters();
                          handleClick();
                        }
                      }}
                      className={`transition-transform duration-150 ${
                      isImpacted ? "scale-95 opacity-80" : ""
                    }`}>
                      submit
                    </Button>
                    <Button variant="ghost" onClick={() => {
                      setTopHeadlines(Filter);
                    }}>reset default</Button>
                  </TabsContent>

                </Tabs>
              </CardContent>
            <CardFooter></CardFooter>
          </Card>
        </div>
      </div>
    </>
  )
}
