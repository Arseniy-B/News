import React from "react"
import { Button } from "@/components/ui/button"
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
import { send_otp, login_by_email } from "../services/api.ts";
import { AxiosError } from 'axios';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSeparator,
  InputOTPSlot,
} from "@/components/ui/input-otp"


const formSchema = z.object({
  email: z.string().min(2).max(50).email("incorrect email format"),
})
type FormData = z.infer<typeof formSchema>;


export default function EmailLoginScreen(){
  const navigate = useNavigate();
  const [open, setOpen] = React.useState<boolean>(false);
  const [value, setValue] = React.useState<string>("");
  const [emailAddress, setEmailAddress] = React.useState<string>("");

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    // try {
      // await send_otp(values.email);
      setEmailAddress(values.email);
      setOpen(true);
    // } catch (e) {
    //   if (e instanceof AxiosError){
    //     if(e.response?.status === 422){
    //       toast(e.response?.data.detail);
    //     }
    //   }
    // }
  }

  async function otpHandler(otpValue: string){
    setValue(otpValue);
    if(otpValue.length === 6){
      try{
        await login_by_email(emailAddress, otpValue)
        navigate("/news")
      } catch(e){
        if(e instanceof AxiosError){
          if(e.response?.status === 422){
            toast(e.response?.data.detail);
          }
        }
      }
    }
  }

  return (
    <>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="h-[300px]">
          <DialogHeader className="m-auto">
            <DialogTitle>
              <InputOTP 
                maxLength={6}
                value={value}
                onChange={otpHandler}
              >
                <InputOTPGroup className="">
                  <InputOTPSlot className="h-12 w-12 text-lg" index={0} />
                  <InputOTPSlot className="h-12 w-12 text-lg" index={1} />
                  <InputOTPSlot className="h-12 w-12 text-lg" index={2} />
                </InputOTPGroup>
                <InputOTPSeparator />
                <InputOTPGroup>
                  <InputOTPSlot className="h-12 w-12 text-lg" index={3} />
                  <InputOTPSlot className="h-12 w-12 text-lg" index={4} />
                  <InputOTPSlot className="h-12 w-12 text-lg" index={5} />
                </InputOTPGroup>
              </InputOTP>
            </DialogTitle>
            <DialogDescription className="font-thin">
              Enter the code sent to your email
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
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
                <div className="w-full mt-10 h-[0.1px] bg-muted rounded-full" />
                <Button type="submit" className="w-full">
                  Send code
                </Button>
              </form>
            </Form>
            <Button onClick={() => {navigate("/auth/sign_in")}} variant="outline" className="w-full mt-10">
              Login with password
            </Button>
          </CardContent>
        </div>
      </Card>
    </>
  )
}
