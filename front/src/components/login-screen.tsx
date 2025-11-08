import React from "react"
import { Button } from "@/components/ui/button"
import { Eye, EyeOff } from "lucide-react";
import {
  Card,
  CardContent,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Toaster, toast } from "sonner"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { z } from "zod";
import { useNavigate } from 'react-router-dom';
import { login_by_password } from "../services/api.ts";
import { AxiosError } from 'axios';


const formSchema = z.object({
  username: z.string().min(2).max(50),
  password: z.string().min(2).max(50),
})
type FormData = z.infer<typeof formSchema>;


export default function LoginScreen(){
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = React.useState(false);

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    try {
      await login_by_password(values.username, values.password);
      navigate("/news")
    } catch (e) {
      if (e instanceof AxiosError){
        if(e.response?.status === 422){
          toast(e.response?.data.detail);
        }
      }
    }
  }

  return (
    <>
      <Toaster />
      <Card className="w-[100%] h-full rounded-none">
        <div className="w-full flex lg:justify-end justify-between px-10" >
          <Button className="lg:hidden" onClick={() => {navigate("/news")}}>News</Button> 
          <Button variant="ghost" onClick={() => navigate("/auth/sign_up")}>Sign up</Button>
        </div>
        <div className="m-[15%] my-auto">
          <CardContent className="my-5">
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                <FormField
                  control={form.control}
                  name="username"
                  render={({ field }) => (
                    <FormItem>
                    <FormControl>
                      <Input placeholder="username" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                  <FormItem>
                    <FormControl>
                      <div className="relative">
                      <Input
                        type={showPassword ? "text" : "password"}
                        placeholder="password"
                        {...field}
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        className="absolute right-2 top-1/2 -translate-y-1/2"
                        onClick={() => setShowPassword(!showPassword)}
                      >
                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      </Button>
                    </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                  )}
                />
                <div className="w-full mt-10 h-[0.1px] bg-muted rounded-full" />
                <Button type="submit" className="w-full">
                  Login
                </Button>
              </form>
            </Form>
            <Button onClick={() => {navigate("/auth/sign_in/email")}} variant="outline" className="w-full mt-10">
              Login by email
            </Button>
          </CardContent>
        </div>
      </Card>
    </>
  )
}
