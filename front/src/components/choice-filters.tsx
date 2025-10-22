import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { filterService, Filter, Category, CountryCode } from "../services/news-api/newsapi";
import React from "react";
import { type BaseFilter } from "../services/news-api/newsapi";


type ChoiceFiltersProps = {
  currentFilter: BaseFilter | null;
  setCurrentFilter: React.Dispatch<React.SetStateAction<BaseFilter | null>>;
}
const ChoiceFilters: React.FC<ChoiceFiltersProps> = ({ currentFilter, setCurrentFilter }) => {
  const [ filter, setFilter ] = React.useState<BaseFilter | null >(null); 

  React.useEffect(() => {
    
  }, []);

  return (
    <>
      <Select>
        <SelectTrigger>
          <SelectValue placeholder={filter} />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectItem value="apple">Apple</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
    </>
  )
}
export default ChoiceFilters;
