const {readdir } = require('fs/promises');

export function readFolder(folderPath: string) {
  try {
    const files = readdir(String.raw`folderPath`);
    files.forEach((file:any) => {
      console.log(file);
    });

  } catch (err) {
    console.error(err);
  }
}
