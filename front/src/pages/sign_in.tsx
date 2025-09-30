import LoginScreen from "@/components/login-screen";


export default function Signin(){
  return (
    <div className="h-screen w-screen grid grid-cols-1 lg:grid-cols-2">
      <div className="bg-muted lg:block hidden"></div>
      <div className="">
        <LoginScreen />
      </div>
    </div>
  )
}
