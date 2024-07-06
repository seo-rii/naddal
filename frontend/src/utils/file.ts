export async function selectFile(): Promise<{ name: string, blob: Blob }> {
    return new Promise<{ name: string, blob: Blob }>((resolve, reject) => {
        const input = document.createElement('input')
        input.type = 'file'
        input.onchange = () => {
            if (input.files?.length) {
                const file = input.files[0]
                const reader = new FileReader()
                reader.onload = () => resolve({name: file.name, blob: new Blob([reader.result as ArrayBuffer])})
                reader.readAsArrayBuffer(file)
            } else reject('No file selected')
        }
        input.click()
    })
}