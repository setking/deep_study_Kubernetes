const VITE_APP_TITLE = import.meta.env.VITE_APP_TITLE ?? "kubernetes"

const dynamicTitle = ref<string>("")

function setTitle(title?: string) {
  dynamicTitle.value = title ? `${VITE_APP_TITLE} | ${title}` : VITE_APP_TITLE

}
watch(dynamicTitle, (value, oldValue) => {
  if (document && value !== oldValue) {
    document.title = value
  }
})

export function useTitle() {
  return {setTitle}
}