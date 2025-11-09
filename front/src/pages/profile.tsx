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
  CardHeader,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useNavigate } from 'react-router-dom';
import { ModeToggle } from "@/components/mode-toggle";
import { getUser, refreshToken, logout, tokenService, getUserFilters, setUserFilters } from "../services/api";
import { useEffect, useState } from "react";
import type { User } from "../services/user-api";
import { format } from 'date-fns';
import type { BaseFilter, TopHeadlinesFilter, EverythingFilter } from '../services/news-api/newsapi';
import { CountryCode, Category, Filter } from '../services/news-api/newsapi';
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


const defaultFilter: Pick<TopHeadlinesFilter, 'pageSize' | 'page'> = {
  pageSize: 20, 
  page: 1,       
};

export default function Profile(){
  const [filters, setFilters] = useState<TopHeadlinesFilter>(Filter);
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null); 

  async function addUser(){
    var res = null;
    try{
    res = await getUser();
    } catch (e) {
      if(e instanceof AxiosError){
        try{
          await refreshToken();
        }catch(e){
          if(e instanceof AxiosError){
            if (e.response?.status === 401){
              navigate("/auth/sign_in/");
            }
            try{
              res = await getUser();
            } catch (e) {
              if(e instanceof AxiosError){
                if(e.response?.status === 401){
                  navigate("/auth/sign_in/");
                }
              }
            }
          }
        }
      }
    }
    if(res){
      setUser(res.data.data);
    }
  }

  async function getFilters(){
    var res = await getUserFilters();
    console.log(res.data);
  }

  useEffect(() => {
    addUser();
    getFilters();
  }, [])

  async function setCurrentUserFilters(){
    console.log(filters)
    var res = await setUserFilters(filters, "TopHeadlines");
    console.log(res);
  }

  async function logoutHandler(){
    await logout();
    tokenService.delete();
    navigate("/auth/sign_in");
  }
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
          <Card className="w-full h-full rounded-[0]">
            <CardHeader>
              
            </CardHeader>
            <CardContent>
              <div className="text-[30px] font-thin flex flex-col">Settings</div>
                <div>theme: <ModeToggle /></div>
                <div>
                  recommendations:<br/>
                    TopHeadlines:
                    <Select onValueChange={(value: CountryCode) => {
                      setFilters({...defaultFilter, ...filters, country: value})    
                    }}>
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder="Country" />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.values(CountryCode).map((code) => (
                          <SelectItem value={code}>{code}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Select onValueChange={(value: Category) => {
                      setFilters({...defaultFilter, ...filters, category: value})    
                    }}>
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder="category" />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.values(Category).map((category) => (
                          <SelectItem value={category}>{category}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Button onClick={setCurrentUserFilters}>submit</Button>
                </div>
              </CardContent>
            <CardFooter></CardFooter>
          </Card>
        </div>
      </div>
    </>
  )
}
