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


export const SearchIn = {
  TITLE: "title",
  DESCRIPTION: "description",
  CONTENT: "content",
}
export type SearchIn = (typeof SearchIn)[keyof typeof SearchIn];


export const Domains = {
  BBC: "bbc.co.uk",
  ECHCRUNCH: "echcrunch.com",
  ENGADGET: "engadget.com"
}
export type Domains = (typeof Domains)[keyof typeof Domains];


export interface BaseFilter{
  pageSize: number;
  page: number;
}


export interface TopHeadlinesFilter extends BaseFilter {
  filter_type: "TopHeadlines";
  country?: CountryCode;
  category?: Category;
  q?: string;
  pageSize: number;
  page: number;
}

export interface EverythingFilter extends BaseFilter {
  filter_type: "Everything";
  from?: Date;
  to?: Date;
  sortBy: SortBy;
  language: Language;
  domains: Domains[];
  searchIn: SearchIn[];
  q?: string;
  pageSize: number;
  page: number;
}

export const Filter: TopHeadlinesFilter = {
  filter_type: "TopHeadlines",
  country: CountryCode.US, 
  pageSize: 20,
  page: 1
};

export const DefaultEverythingFIlter: EverythingFilter = {
  filter_type: "Everything",
  sortBy: SortBy.POPULARITY,
  language: Language.EN,
  domains: [Domains.BBC, Domains.ENGADGET, Domains.ECHCRUNCH],
  searchIn: [SearchIn.TITLE, SearchIn.CONTENT, SearchIn.DESCRIPTION],
  pageSize: 20,
  page: 1,
}

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
