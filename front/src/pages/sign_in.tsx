import { login } from "../services/api.ts";
import { Button } from "@/components/ui/button"


export default function Signin(){
  async function clickHandler(){
    try {
      const res = await login("string", "string");
      console.log("Пользователь:", res.data);
    } catch (e) {
      console.error("Ошибка при получении пользователя");
    }
  }

  return (
    <>
      <Button onClick={clickHandler}>Sign in</Button>
    </>
  )
}
