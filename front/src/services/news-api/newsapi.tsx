export type Source = {
  id?: string;
  name?: string;
}

export type NewsItem = {
  source: Source;
  author?: string | null;
  title: string;
  description?: string | null;
  url?: string | null;
  urlToImage?: string | null;
  publishedAt: string; 
  content?: string | null;
}

export const CountryCode = {
  US: "US",
  RU: "RU",
  CN: "CN",
  GB: "GB",
  DE: "DE",
  FR: "FR",
  JP: "JP",
  IN: "IN",
  BR: "BR",
  CA: "CA", 
  AU: "AU", 
  IT: "IT",
  ES: "ES",
  KR: "KR",
  MX: "MX",
} as const;
export type CountryCode = (typeof CountryCode)[keyof typeof CountryCode];

export const Category = {
  BUSINESS: "business",
  ENTERTAINMENT: "entertainment",
  GENERAL: "general",
  HEALTH: "health",
  SCIENCE: "science",
  SPORTS: "sports",
  TECHNOLOGY: "technology",
} as const;
export type Category = (typeof Category)[keyof typeof Category];

export const SortBy = {
  RELEVANCY: "relevancy",
  POPULARITY: "popularity",
  PUBLISHED_AT: "publishedAt",
}
export type SortBy = (typeof SortBy)[keyof typeof SortBy];

export const Language = {
  AR: "ar",
  DE: "de",
  EN: "en",
  ES: "es",
  FR: "fr",
  HE: "he",
  IT: "it",
  NL: "nl",
  NO: "no",
  PT: "pt",
  RU: "ru",
  SV: "sv",
  UD: "ud",
  SH: "sh"
}
export type Language = (typeof Language)[keyof typeof Language];


export interface BaseFilter{
  pageSize: number;
  page: number;
}


export interface TopHeadlinesFilter extends BaseFilter {
  country?: CountryCode;
  category?: Category;
  q?: string;
  pageSize: number;
  page: number;
}

export interface EverythingFilter extends BaseFilter {
  from?: Date;
  to?: Date;
  sortBy: SortBy;
  language: Language;
  domains: string
  q?: string;
  pageSize: number;
  page: number;
}

export const Filter: TopHeadlinesFilter = {
  country: CountryCode.US, 
  // category: Category.BUSINESS,
  // q: "экономика",
  pageSize: 20,
  page: 1
};

const USER_FILTER_KEY = "filters"

export const filterService = {
  set(filters: BaseFilter) {
    const jsonFilters = JSON.stringify(filters, null, 2);
    localStorage.setItem(USER_FILTER_KEY, jsonFilters);
  },

  get(): BaseFilter | null {
    const jsonFilters = localStorage.getItem(USER_FILTER_KEY);
    if (jsonFilters){
      const filters: TopHeadlinesFilter = JSON.parse(jsonFilters);
      return filters;
    }
    return null;
  },
}; 
