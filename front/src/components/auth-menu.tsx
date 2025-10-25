import { tokenService, refreshToken } from "../services/api";
import { Button } from "@/components/ui/button";
import { HatGlasses, LogIn } from "lucide-react";
import { useNavigate } from 'react-router-dom';
import { decodeJwt, type JwtPayload } from "../services/jwt-decode";
import React from "react";


export default function AuthMenu(){
  const token = tokenService.get();
  const tokenPayload: JwtPayload | null = token ? decodeJwt(token) : null;
  const navigate = useNavigate();

  const [isAuthenticated, setIsAuthenticated] = React.useState<boolean>(false);

  React.useEffect(() => {
    if(tokenPayload && tokenPayload.exp > Math.floor(Date.now() / 1000)){
      setIsAuthenticated(true);
    }
    async function checkAuthenticated(){
      const res = await refreshToken()
      if(res.data.status_code >= 200 && res.data.status_code <= 299){
        setIsAuthenticated(true);
      }
    }
    checkAuthenticated();
  }, []);

  if (isAuthenticated) {
    return (
      <>
        <Button variant="ghost" onClick={() => {navigate("/user/profile")}}>
          <HatGlasses />
        </Button>
      </>
    )
  }

  return (
    <>
      <Button variant="ghost" onClick={() => {navigate("/auth/sign_in")}}><LogIn /></Button>
    </>
  )
}
