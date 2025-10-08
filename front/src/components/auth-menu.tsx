import { tokenService } from "../services/api";
import { Button } from "@/components/ui/button";
import { HatGlasses } from "lucide-react";
import { useNavigate } from 'react-router-dom';


export default function AuthMenu(){
  const token = tokenService.get();
  const navigate = useNavigate();

  if (token) {
    return (
      <>
        <Button variant="outline" onClick={() => {navigate("/auth/prifile")}}>
          <HatGlasses />
        </Button>
      </>
    )
  }

  return (
    <>
      <Button variant="secondary" onClick={() => {navigate("/auth/sign_in")}}>Auth</Button>
    </>
  )
}
