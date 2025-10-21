import { tokenService } from "../services/api";
import { Button } from "@/components/ui/button";
import { HatGlasses, LogIn } from "lucide-react";
import { useNavigate } from 'react-router-dom';
import { decodeJwt, type JwtPayload } from "../services/jwt-decode";


export default function AuthMenu(){
  const isToken = tokenService.get();
  const navigate = useNavigate();

  if (isToken) {
    return (
      <>
        <Button variant="outline" onClick={() => {navigate("/user/profile")}}>
          <HatGlasses />
        </Button>
      </>
    )
  }

  return (
    <>
      <Button variant="secondary" onClick={() => {navigate("/auth/sign_in")}}><LogIn /></Button>
    </>
  )
}
