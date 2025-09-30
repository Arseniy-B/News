import type { FormEvent } from 'react';
import { Button } from "@/components/ui/button"
import {
  Card,
  CardAction,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

import { useNavigate } from 'react-router-dom';
import { login } from "../services/api.ts";


export default function LoginScreen(){
  const navigate = useNavigate();

  async function clickHandler(event: FormEvent<HTMLFormElement>){
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const data: Record<string, >FormDataEntryValue = Object.fromEntries(formData);
    try {
      const res = await login("string", "string");
      if (res.data.success === "True"){
        navigate("/")
      }
      console.log("Пользователь:", res.data);
    } catch (e) {
      console.error("Ошибка при получении пользователя");
    }
  }

  return (
    <>
      <Card className="w-[100%] h-full rounded-none">
        <div className="w-full flex justify-end pr-10">Sign up</div>
        <div className="m-auto">
          <CardContent className="my-5">
            <form>
              <div className="flex flex-col gap-6">
                <div className="grid gap-2">
                  <Label htmlFor="login">Username</Label>
                  <Input
                    id="login"
                    type="login"
                    // placeholder="m@example.com"
                    required
                  />
                </div>
                <div className="grid gap-2">
                  <div className="flex items-center">
                    <Label htmlFor="password">Password</Label>
                    <a
                      href="#"
                      className="ml-20 inline-block text-sm underline-offset-4 hover:underline"
                    >
                      Forgot your password?
                    </a>
                  </div>
                  <Input id="password" type="password" required />
                </div>
              </div>
            </form>
          </CardContent>
          <CardFooter className="flex-col gap-2">
            <Button onClick={clickHandler} type="submit" className="w-full">
              Login
            </Button>
            <Button variant="outline" className="w-full">
              Login with Google
            </Button>
          </CardFooter>    
        </div>
      </Card>
    </>
  )
}
