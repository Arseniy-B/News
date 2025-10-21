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
import { getUser } from "../services/api";
import { useEffect, useState } from "react";
import type { AxiosResponse } from 'axios';
import type { User } from "../services/user-api";


export default function Profile(){
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null); 

  async function addUser(){
    const res = await getUser() as AxiosResponse<User>;
    setUser(res.data);
  }
  useEffect(() => {
    addUser();
  }, [])

  return (
    <>
      <div className="fixed w-full p-5 flex justify-end">
        <Button variant="ghost" onClick={() => navigate("/news")}>News</Button>
      </div>
      <div className="h-[100vh] grid lg:grid-cols-7">
        <div className="col-span-4 lg:col-span-3 pl-[10vw] bg-secondary flex flex-col font-thin text-[20px]">
          <div className="h-[30vh]"></div>
          <div>username: {user?.username} </div>
          <div>email: {user?.email}</div>
          <div>created at: </div>
        </div>
        <div className="col-span-4">
          <Card className="w-full h-full rounded-[0]">
            <CardHeader>
              
            </CardHeader>
            <CardContent>
              <div className="text-[30px] font-thin flex flex-col">Settings</div>
                <div>theme: <ModeToggle /></div>
                <div>
                  news api:
                  <Select>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="NewsApi" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value={"NewsApi"}>{"NewsApi"}</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
            </CardContent>
            <CardFooter></CardFooter>
          </Card>
        </div>
      </div>
    </>
  )
}
