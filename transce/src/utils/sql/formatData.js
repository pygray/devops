export function CascaderData(dbs) {
  const formatDataList = []
  for (const i in dbs) {
    const itemb = dbs[i]
    if (formatDataList.length === 0) {
      const data = {
        value: itemb.cluster_id,
        label: itemb.cluster_name,
        children: [
          {
            value: itemb.env,
            label: itemb.env,
            children: [
              {
                value: itemb.id,
                label: itemb.name
              }
            ]
          }
        ]
      }
      formatDataList.push(data)
    } else {
      let tag = 0
      for (const j in formatDataList) {
        const itema = formatDataList[j]
        if (itemb.cluster_name === itema.label) {
          const env_children = itema.children
          if (env_children.length === 2) {
            for (const m in env_children) {
              const env_item = env_children[m]
              if (env_item.value === itemb.env) {
                const host = { value: itemb.id, label: itemb.name }
                env_item.children.push(host)
                break
              }
            }
          } else if (env_children.length === 1) {
            const env_children0 = env_children[0]
            if (env_children0.value === itemb.env) {
              const host = { value: itemb.id, label: itemb.name }
              env_children0.children.push(host)
            } else {
              const data =
                {
                  value: itemb.env,
                  label: itemb.env,
                  children: [
                    {
                      value: itemb.id,
                      label: itemb.name
                    }
                  ]
                }
              env_children.push(data)
            }
          }
          tag = 1
          break
        }
      }
      if (tag === 0) {
        const data = 	{
          value: itemb.cluster_id,
          label: itemb.cluster_name,
          children: [
            {
              value: itemb.env,
              label: itemb.env,
              children: [
                {
                  value: itemb.id,
                  label: itemb.name
                }
              ]
            }
          ]
        }
        formatDataList.push(data)
      }
    }
  }
  return formatDataList
}
