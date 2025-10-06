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
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { z } from "zod";
import { useNavigate } from 'react-router-dom';
import { register } from "../services/api.ts";


const formSchema = z.object({
  username: z.string().min(2).max(50),
  email: z.string().min(5).max(100),
  password1: z.string().min(2).max(50),
  password2: z.string().min(2).max(50),
})
.refine((data) => data.password1 === data.password2, {
  path: ["password2"], // укажем, где показывать ошибку
  message: "passwords must be the same",
});

type FormData = z.infer<typeof formSchema>;

export default function RegisterScreen(){
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = React.useState(false);

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      email: "",
      password1: "",
      password2: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    console.log(values)
    try {
      const res = await register(values.username, values.email, values.password1);
      if (res.data.success === "True"){
        navigate("/news")
      }
      console.log("Пользователь:", res.data);
    } catch (e) {
      console.error("Ошибка при получении пользователя");
    }
  }

  return (
    <>
      <Card className="w-[100%] h-full rounded-none">
        <div className="w-full flex justify-end pr-10" >
          <Button variant="ghost" onClick={() => navigate("/auth/sign_in")}>Sign in</Button>
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
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                    <FormControl>
                      <Input placeholder="email" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="password1"
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
                <FormField
                  control={form.control}
                  name="password2"
                  render={({ field }) => (
                  <FormItem>
                    <FormControl>
                      <div className="relative">
                      <Input
                        type={showPassword ? "text" : "password"}
                        placeholder="confirm password"
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
                  sign up
                </Button>
                <Button  variant="outline" className="w-full">
                  Sign up with Google
                </Button>
              </form>
            </Form>
          </CardContent>
        </div>
      </Card>
    </>
  )
}
