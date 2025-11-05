import { request } from "@/http/axios"
import type * as Files from "./type"

/** 查 */
export function getFilesApi() {
  return request<Files.FilesResponseData>({
    url: "/api/files",
    method: "get",
  })
}
