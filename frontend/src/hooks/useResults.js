

import json from "../db/obj.json";

export function useResults (){
    const results = json
    const mappedResults = results?.map(res => ({
      id: res.id,
      title: res.title,
      content: res.content,
      url: res.url
    }))
    return {results: mappedResults}
  }