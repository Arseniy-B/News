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
import type { User } from "../services/user-api";
import { format } from 'date-fns';


export default function Profile(){
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null); 

  async function addUser(){
    var res = null;
    res = await getUser();
    if( res.data.status_code === 401){
      navigate("/auth/sign_in");
    }
    setUser(res.data.data);
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
