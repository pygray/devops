export const dateOption = {
  shortcuts: [
    {
      text: '1 周',
      onClick(picker) {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
        return picker.$emit('pick', [start, end])
      }
    },
    {
      text: '1 月',
      onClick(picker) {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
        return picker.$emit('pick', [start, end])
      }
    },
    {
      text: '3 月',
      onClick(picker) {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
        return picker.$emit('pick', [start, end])
      }
    }
  ]
}
const baseData = {
  dateOption: dateOption
}
export default baseData
