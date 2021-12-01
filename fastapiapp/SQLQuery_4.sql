SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Language](
	[languageid] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](40) NOT NULL,
	[origin] [varchar](max) NOT NULL,
	[description] [varchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[languageid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

INSERT INTO Language (name, origin) VALUES ('chinois', 'sinitic')
INSERT INTO Language (name, origin) VALUES ('francais', 'indo european')

INSERT INTO Language (name, origin) VALUES ('espangole', 'indo european')

select * from [Language];